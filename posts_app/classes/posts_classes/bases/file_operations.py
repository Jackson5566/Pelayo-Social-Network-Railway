from abc import ABC
from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.model_operations import ModelOperations
from api.classes.type_alias.operations import Operations
from posts_app.models import FileModel


class FileOperations(Operations, ABC):

    def __init__(self, request, model_id=None, model_instance=None):
        ControllerLogicExecutor.__init__(self, request=request)
        ModelOperations.__init__(self, model_id=model_id, model_instance=model_instance, model_class=FileModel)
