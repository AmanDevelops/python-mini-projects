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
                self.posts = pickle.load(f).posts
        except:
            self.posts = []

    @write_file
    def add_post(self, title: str, date: str, content: str):
        post = {
            "id": len(self.posts) + 1,
            "title": title,
            "date": date,
            "content": content,
        }

        self.posts.append(post)

    @write_file
    def update_post(self, id: int, title: str, date: str, content: str):
        self.posts[id - 1] = {
            "id": id,
            "title": title,
            "date": date,
            "content": content,
        }
        print(self.posts)

    @write_file
    def delete_post(self, id: int):
        self.posts.pop(id - 1)

    def get_post(self, id: int) -> dict:
        return self.posts[id - 1]
