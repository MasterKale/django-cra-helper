from cra_helper import STATIC_ASSET_MANIFEST


def static(request):
    if STATIC_ASSET_MANIFEST:
        return STATIC_ASSET_MANIFEST

    return {}
