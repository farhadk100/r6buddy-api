from deta import Deta

from core.config import settings

deta = Deta(settings.DETA_PROJECT_KEY)
db = {
    "operators": deta.Base("r6buddy-operators"),
    "weapons": deta.Base("r6buddy-weapons"),
    "gadgets": deta.Base("r6buddy-gadgets"),
}
