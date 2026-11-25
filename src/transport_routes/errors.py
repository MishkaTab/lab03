class CatalogError(Exception):
    pass

class WrongRoute(CatalogError):
    pass

class DuplicateId(CatalogError):
    pass

class NotFoundObject(CatalogError):
    pass

class UnsupportedFormatVersion(CatalogError):
    pass

class DamagedFile(CatalogError):
    pass