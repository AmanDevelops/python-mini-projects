import requests


class Summarizer:
    """
    Summarizes a Github Profile for recent Events
    """

    CURRENT_SUPPORTED_EVENTS = (
        "PushEvent",
        "IssuesEvent",
        "WatchEvent",
        "PullRequestEvent",
    )

    def __init__(self) -> None:
        self.summary: dict[
            str, dict[str, int] | dict[str, dict[str, int]] | list[str]
        ] = {
            "pushEvent": {
                # "repoName": count
            },
            "issuesEvent": {
                # "actionType": {
                #   "repoName": count
                # }
            },
            "watchEvent": [
                # repoName
            ],
            "PullRequestEvent": {
                # "actionType": {
                #   "repoName": count
                # }
            },
        }

    def PushEvent(self, event: dict) -> None:
        """
        Docs: https://docs.github.com/en/rest/using-the-rest-api/github-event-types#pushevent
        """

        repo_name = event["repo"]["name"]
        self.summary["pushEvent"][repo_name] = (
            self.summary["pushEvent"].get(repo_name, 0) + 1
        )

    def IssuesEvent(self, event: dict) -> None:
        """
        Docs: https://docs.github.com/en/rest/using-the-rest-api/github-event-types#issuesevent
        """

        action = event["payload"]["action"]
        repo_name = event["repo"]["name"]

        if action not in self.summary["issuesEvent"]:
            self.summary["issuesEvent"][action] = {}

        current_issues_count = self.summary["issuesEvent"][action].get(repo_name, 0)

        self.summary["issuesEvent"][action][repo_name] = current_issues_count + 1

    def WatchEvent(self, event: dict) -> None:
        """
        Docs: https://docs.github.com/en/rest/using-the-rest-api/github-event-types#watchevent
        """

        self.summary["watchEvent"].append(event["repo"]["name"])

    def PullRequestEvent(self, event: dict) -> None:
        """
        Docs: https://docs.github.com/en/rest/using-the-rest-api/github-event-types#pullrequestevent
        """

        action = event["payload"]["action"]
        repo_name = event["repo"]["name"]

        if action not in self.summary["PullRequestEvent"]:
            self.summary["PullRequestEvent"][action] = {}

        current_pr_count = self.summary["PullRequestEvent"][action].get(repo_name, 0)
        self.summary["PullRequestEvent"][action][repo_name] = current_pr_count + 1

    def summarize(self, username: str):
        """
        Prints the summary based on self.summary
        """

        eventsResponse = requests.get(f"https://api.github.com/users/{username}/events")

        if not eventsResponse.ok:
            error_message = eventsResponse.json()
            print(
                f"[Error {error_message.get('status')}]: {error_message.get('message')}"
            )
            return

        events = eventsResponse.json()

        # Processing the result from APi
        for event in events:
            event_type = event.get("type")
            if event_type not in self.CURRENT_SUPPORTED_EVENTS:
                continue

            handler = getattr(self, event_type, None)
            if handler:
                handler(event=event)

        # Printing the summarized result
        print(f"Here is the recent activities of {username}: \n")

        for event_type, event_summary_data in self.summary.items():
            if not event_summary_data:
                continue

            if event_type == "pushEvent":
                print("Commits: ")
                for repo_name, number_of_commits in event_summary_data.items():
                    print(
                        f"    - Pushed {number_of_commits} commits to {repo_name}"
                    )

            elif event_type == "issuesEvent":
                print("Issues: ")
                for action_type, repos in event_summary_data.items():
                    for repo_name, count in repos.items():
                        print(f"    - {action_type} {count} issue in {repo_name}")

            elif event_type == "watchEvent":
                print("Stars: ")
                for i in event_summary_data:
                    print(f"    - Starred {i}")

            elif event_type == "PullRequestEvent":
                print("Pull Request: ")
                for action_type, repos in event_summary_data.items():
                    for repo_name, count in repos.items():
                        print(
                            f"    - {action_type} {count} pull request in {repo_name}"
                        )
