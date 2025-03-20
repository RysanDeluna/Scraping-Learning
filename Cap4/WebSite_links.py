class WebSite:
    """
    Structure of a website
    """

    def __init__(self, name, url, target_pattern, absolute_url, title_tag, body_tag):
        self.name = name
        self.url = url
        self.target_pattern = target_pattern
        self.absolute_url = absolute_url
        self.title_tag = title_tag
        self.body_tag = body_tag


    def get_name(self):
        return self.name

    def get_url(self):
        return self.url

    def get_title_tag(self):
        return self.title_tag

    def get_body_tag(self):
        return self.body_tag

class Content:
    """
    Base class common to every article or page
    """

    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        """
        Simple macro for exhibition
        """
        print(
            "---" * 20 + "\n"
            "URL: {}\n"
            "TITLE: {}\n"
            "BODY: \n{}".format(self.url, self.title, self.body)
        )