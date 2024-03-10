from base.constants import BaseConstant


class EventStatus(BaseConstant):
    Created = "created"
    Canceled = "canceled"
    OnGoing = "ongoing"
    Completed = "completed"


class SaveEventConstant(BaseConstant):
    Saved = "Saved"
    Removed = "Removed"
