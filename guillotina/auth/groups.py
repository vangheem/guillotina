from guillotina import configure
from guillotina.auth.users import GuillotinaUser
from guillotina.interfaces import IGroups
from guillotina.interfaces import IPrincipal

import typing


class GuillotinaGroup(GuillotinaUser):
    pass


@configure.utility(provides=IGroups)
class GroupsUtility:
    """ Class used to get groups. """

    def __init__(self):
        self._managers_group = GuillotinaGroup(
            roles={
                "guillotina.ContainerAdmin": 1,
                "guillotina.ContainerDeleter": 1,
                "guillotina.Owner": 1,
                "guillotina.Member": 1,
                "guillotina.Manager": 1,
            }
        )

        self._groups: typing.Dict[str, GuillotinaGroup] = {"Managers": self._managers_group}

    async def load_groups(self, groups):
        pass

    def get_principal(self, ident: str, principal: typing.Optional[IPrincipal]) -> IPrincipal:
        return self._groups.get(ident) or GuillotinaGroup()
