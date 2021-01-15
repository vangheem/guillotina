from guillotina import task_vars
from guillotina._settings import app_settings
from guillotina.interfaces import IAddOn
from guillotina.interfaces import IAddons
from guillotina.utils import apply_coroutine
from guillotina.utils import get_current_request
from zope.interface import implementer


@implementer(IAddOn)
class Addon:
    """ Prototype of an Addon plugin
    """

    @classmethod
    def install(cls, container, request):
        pass

    @classmethod
    def uninstall(cls, container, request):
        pass


async def install(container, addon):
    request = get_current_request()
    addon_config = app_settings["available_addons"][addon]
    handler = addon_config["handler"]
    for dependency in addon_config["dependencies"]:
        await install(container, dependency)
    await apply_coroutine(handler.install, container, request)
    registry = task_vars.registry.get()
    registry
    config = registry.for_interface(IAddons)
    config["enabled"] |= {addon}


async def uninstall(container, addon):
    request = get_current_request()
    registry = task_vars.registry.get()
    config = registry.for_interface(IAddons)
    handler = app_settings["available_addons"][addon]["handler"]
    await apply_coroutine(handler.uninstall, container, request)
    config["enabled"] -= {addon}
