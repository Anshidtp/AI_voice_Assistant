import enum
from typing import Annotated
from livekit.agents import llm
import logging

logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)

class Zone(enum.Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    OFFICE = "office"

class AssistantFunc(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()

        self.temperature = {
            Zone.LIVING_ROOM: 22,
            Zone.BEDROOM: 20,
            Zone.KITCHEN : 23,
            Zone.BATHROOM: 22,
            Zone.OFFICE:21 

        }
    
    @llm.ai_callable(description="get the temperature in a specific room")
    def get_temperature(self,zone:Annotated[Zone,llm.TypeInfo(description=" The Specific Zone")]):
        logger.info("get temp - Zone %s",zone)
        temp = self._temperature[Zone(zone)]
        return f"The Temperature in the {zone} is {temp} C"
