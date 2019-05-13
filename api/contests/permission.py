from rest_framework import permissions

from .models import RegistContestUser, Contest, Submittion


class IsRegistedContest(permissions.BasePermission):
    """
    コンテストに参加登録しているかを見る
    """

    def has_permission(self, request, view):
        """
        contest_tagとusernameをみてcontest_registに入ってたらOK
        """
        tag = view.kwargs.get("contest_tag")
        username = request.user.username  # requestにusernameが含まれている体
        perm = RegistContestUser.objects.filter(contest_tag=tag,
                                                username=username).exists()
        return perm


class IsActiveContest(permissions.BasePermission):
    """
    コンテストがアクティブだった場合,
    参加登録してるかを見る
    """
    def has_permission(self, request, view):
        tag = view.kwargs.get("contest_tag")
        username = request.user.username  # requestにusernameが含まれている体

        perm1 = Contest.objects.filter(contest_tag=tag,
                                       is_open=True,
                                       is_active=True).exists()
        if perm1:
            perm2 = RegistContestUser.objects.filter(contest_tag=tag,
                                                     username=username
                                                     ).exists()
            return perm2
        else:  # activeじゃなかったらOK
            return True


class IsActive(permissions.BasePermission):
    """ activeだったら自分ののみ """
    def has_permission(self, request, view):
        tag = view.kwargs.get("contest_tag")
        id_ = view.kwargs.get("problem_id")
        perm1 = Contest.objects.filter(contest_tag=tag,
                                       is_open=True,
                                       is_active=True).exists()
        if perm1:
            username = request.user.username
            if Submittion.objects.filter(id=id_, author=username).exists():
                return True
            else:
                return False
        else:
            return True


class IsScheduleContest(permissions.BasePermission):
    """ コンテストが予約されているものかをみる
    予約されていたらだめ！なのでpermを否定している
    """

    def has_permission(self, request, view):
        tag = view.kwargs.get("contest_tag")
        perm = Contest.objects.filter(contest_tag=tag,
                                      is_schedule=True).exists()
        return not perm
