import pickle


class Database:
    def write_file(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            try:
                with open("posts.pkl", "wb") as file:
                    pickle.dump(self, file)
            except:
                raise IOError("Could not write data to file")
            return result

        return wrapper

    def __init__(self):
        try:
            with open("posts.pkl", "rb") as f:
                temp_instance = pickle.load(f)
                self.posts = temp_instance.posts
                self.index = temp_instance.index
        except:
            self.posts = []
            self.index = 0

    @write_file
    def add_post(self, title: str, date: str, content: str):
        post = {
            "id": self.index + 1,
            "title": title,
            "date": date,
            "content": content,
        }

        self.posts.append(post)
        self.index += 1

    @write_file
    def update_post(self, id: int, title: str, date: str, content: str):
        post_index = self.posts.index(
            next((post for post in self.posts if post.get("id") == id), None)
        )
        self.posts[post_index] = {
            "id": id,
            "title": title,
            "date": date,
            "content": content,
        }
        print(self.posts)

    @write_file
    def delete_post(self, id: int):

        self.posts.pop(
            self.posts.index(
                next((post for post in self.posts if post.get("id") == id), None)
            )
        )

    def get_post(self, id: int) -> dict:
        return next((post for post in self.posts if post.get("id") == id), None)
