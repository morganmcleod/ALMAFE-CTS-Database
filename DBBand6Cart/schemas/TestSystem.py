from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# CREATE TABLE `TestSystems` (
# `keyTestSystems` INT(20) NOT NULL AUTO_INCREMENT,
# `fkTestSystemName` INT(20) NULL DEFAULT NULL,
# `TS` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

# CREATE TABLE `TestSystemNames` (
# `keyTestSystemNames` INT(20) NOT NULL AUTO_INCREMENT,
# `Name` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
# `TS` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

class TestSystem(BaseModel):
    key: int = 0
    name: str = ""
    timeStamp: datetime
