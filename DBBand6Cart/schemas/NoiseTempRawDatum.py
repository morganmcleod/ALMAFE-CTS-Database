from pydantic import BaseModel
from datetime import datetime
from enum import Enum

# CREATE TABLE `NT_Raw_Data` (
# 	`keyNT_Raw_Data` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
# 	`fkCartTest` INT(10) UNSIGNED NOT NULL DEFAULT '0',
# 	`fkDUT_Type` INT(10) UNSIGNED NULL DEFAULT '0',
# 	`fkNT_Calc_Data` INT(10) UNSIGNED NULL DEFAULT NULL,
# 	`TS` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
# 	`FreqLO` DOUBLE(10,6) NOT NULL DEFAULT '0.000000',
# 	`CenterIF` DOUBLE(10,6) NOT NULL DEFAULT '0.000000',
# 	`BWIF` FLOAT(7,3) NOT NULL DEFAULT '100.000',
# 	`Pol` TINYINT(3) UNSIGNED NOT NULL DEFAULT '0',
# 	`PwrUSB_SrcLSB` FLOAT NULL DEFAULT NULL,
# 	`PwrLSB_SrcLSB` FLOAT NULL DEFAULT NULL,
# 	`PwrUSB_SrcUSB` FLOAT NULL DEFAULT NULL,
# 	`PwrLSB_SrcUSB` FLOAT NULL DEFAULT NULL,
# 	`Phot_LSB` FLOAT NULL DEFAULT NULL,
# 	`Pcold_LSB` FLOAT NULL DEFAULT NULL,
# 	`Phot_LSB_StdErr` FLOAT NULL DEFAULT NULL,
# 	`Pcold_LSB_StdErr` FLOAT NULL DEFAULT NULL,
# 	`LSB_Pass` TINYINT(3) UNSIGNED NULL DEFAULT NULL,
# 	`Phot_USB` FLOAT NULL DEFAULT NULL,
# 	`Pcold_USB` FLOAT NULL DEFAULT NULL,
# 	`Phot_USB_StdErr` FLOAT NULL DEFAULT NULL,
# 	`Pcold_USB_StdErr` FLOAT NULL DEFAULT NULL,
# 	`USB_Pass` TINYINT(3) UNSIGNED NULL DEFAULT NULL,
# 	`TRF_Hot` FLOAT NULL DEFAULT NULL,
# 	`IF_Attn` INT(10) UNSIGNED NULL DEFAULT NULL,
# 	`Vj1` FLOAT NULL DEFAULT NULL,
# 	`Ij1` FLOAT NULL DEFAULT NULL,
# 	`Vj2` FLOAT NULL DEFAULT NULL,
# 	`Ij2` FLOAT NULL DEFAULT NULL,
# 	`Imag` FLOAT NULL DEFAULT NULL,
# 	`Tmixer` FLOAT NULL DEFAULT NULL,
# 	`PLL_Lock_V` FLOAT NULL DEFAULT NULL,
# 	`PLL_Corr_V` FLOAT NULL DEFAULT NULL,
# 	`PLL_Assm_T` FLOAT NULL DEFAULT NULL,
# 	`PA_A_Drain_V` FLOAT NULL DEFAULT NULL,
# 	`PA_B_Drain_V` FLOAT NULL DEFAULT NULL,
# 	`Source_Power` FLOAT UNSIGNED NULL DEFAULT NULL COMMENT 'BEAST PA_A on CTS, Keithly Current on MTS',
# 	`flag` INT(10) NOT NULL DEFAULT '1',
# 	`OldfkCartTest` INT(10) NOT NULL DEFAULT '0',
# 	PRIMARY KEY (`keyNT_Raw_Data`) USING BTREE
# )

class DUT_Types(Enum):
    BAND6_CARTRIDGE = 0
    MIXER_PREAMP = 1

# from NT_Raw_Data:
COLUMNS = ( 
    'keyNT_Raw_Data',
    'fkCartTest',
    'fkDUT_Type',
    'TS',
    'FreqLO',
    'CenterIF',
    'BWIF',
    'Pol',
    'PwrUSB_SrcLSB',
    'PwrLSB_SrcLSB',
    'PwrUSB_SrcUSB',
    'PwrLSB_SrcUSB',
    'Phot_LSB',
    'Pcold_LSB',
    'Phot_LSB_StdErr',
    'Pcold_LSB_StdErr',
    'Phot_USB',
    'Pcold_USB',
    'Phot_USB_StdErr',
    'Pcold_USB_StdErr',
    'TRF_Hot',
    'IF_Attn',
    'Vj1',
    'Ij1',
    'Vj2',
    'Ij2',
    'Imag',
    'Tmixer',
    'PLL_Lock_V',
    'PLL_Corr_V',
    'PLL_Assm_T',
    'PA_A_Drain_V',
    'PA_B_Drain_V',
    'Source_Power' 
)

class NoiseTempRawDatum(BaseModel):
    key: int = 0                  # keyNT_Raw_Data normally assigned by the server on insert
    fkCartTest: int
    fkDUT_Type: DUT_Types
    timeStamp: datetime = None
    FreqLO: float
    CenterIF: float
    BWIF: float
    Pol: int
    PwrUSB_SrcLSB: float
    PwrLSB_SrcLSB: float
    PwrUSB_SrcUSB: float
    PwrLSB_SrcUSB: float
    Phot_LSB: float
    Pcold_LSB: float
    Phot_LSB_StdErr: float
    Pcold_LSB_StdErr: float
    Phot_USB: float
    Pcold_USB: float
    Phot_USB_StdErr: float
    Pcold_USB_StdErr: float
    TRF_Hot: float
    IF_Attn: int
    Vj1: float
    Ij1: float
    Vj2: float
    Ij2: float
    Imag: float
    Tmixer: float
    PLL_Lock_V: float
    PLL_Corr_V: float
    PLL_Assm_T: float
    PA_A_Drain_V: float
    PA_B_Drain_V: float
    Source_Power : float
    
    def getInsertVals(self):
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()
        return "{},{},{},'{}',{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
            self.fkCartTest,
            self.fkDUT_Type,
            self.timeStamp,
            self.FreqLO,
            self.CenterIF,
            self.BWIF,
            self.Pol,
            self.PwrUSB_SrcLSB,
            self.PwrLSB_SrcLSB,
            self.PwrUSB_SrcUSB,
            self.PwrLSB_SrcUSB,
            self.Phot_LSB,
            self.Pcold_LSB,
            self.Phot_LSB_StdErr,
            self.Pcold_LSB_StdErr,
            self.Phot_USB,
            self.Pcold_USB,
            self.Phot_USB_StdErr,
            self.Pcold_USB_StdErr,
            self.TRF_Hot,
            self.IF_Attn,
            self.Vj1,
            self.Ij1,
            self.Vj2,
            self.Ij2,
            self.Imag,
            self.Tmixer,
            self.PLL_Lock_V,
            self.PLL_Corr_V,
            self.PLL_Assm_T,
            self.PA_A_Drain_V,
            self.PA_B_Drain_V,
            self.Source_Power 
        )