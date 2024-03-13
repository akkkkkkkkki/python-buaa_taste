from backend import get_all_tags


class TagsModel:

    @staticmethod
    def get_all():
        return get_all_tags()
