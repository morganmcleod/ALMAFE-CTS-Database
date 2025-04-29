from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from .DUT_Type import DUT_Type

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
# 	`Source_Power_USB` FLOAT UNSIGNED NULL DEFAULT NULL COMMENT 'BEAST PA_A on CTS, Keithly Current on MTS',
# 	`Source_Power_LSB` FLOAT NOT NULL DEFAULT '1',
# 	`Is_LO_Unlocked` TINYINT(4) NOT NULL DEFAULT '1',
# 	`Is_RF_Unlocked` TINYINT(4) NOT NULL DEFAULT '1',
# 	`flag` INT(10) NOT NULL DEFAULT '1',
# 	`OldfkCartTest` INT(10) NOT NULL DEFAULT '0',
# 	PRIMARY KEY (`keyNT_Raw_Data`) USING BTREE,
# 	INDEX `fkCartTest` (`fkCartTest`) USING BTREE
# )

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
    'Source_Power_USB',
    'Source_Power_LSB',
    'Is_LO_Unlocked',
    'Is_RF_Unlocked'
)

class NoiseTempRawDatum(BaseModel):
    key: int = 0                  # keyNT_Raw_Data normally assigned by the server on insert
    fkCartTest: int = 0
    fkDUT_Type: DUT_Type = DUT_Type.Band6_Cartridge
    timeStamp: datetime = None
    FreqLO: float = 0
    CenterIF: float = 0
    BWIF: float = 0
    Pol: int = 0
    PwrUSB_SrcLSB: float = 0
    PwrLSB_SrcLSB: float = 0
    PwrUSB_SrcUSB: float = 0
    PwrLSB_SrcUSB: float = 0
    Phot_LSB: float = 0
    Pcold_LSB: float = 0
    Phot_LSB_StdErr: float = 0
    Pcold_LSB_StdErr: float = 0
    Phot_USB: float = 0
    Pcold_USB: float = 0
    Phot_USB_StdErr: float = 0
    Pcold_USB_StdErr: float = 0
    TRF_Hot: float = 0
    IF_Attn: int = 0
    TColdLoad: float = 0
    Vj1: float = 0
    Ij1: float = 0
    Vj2: float = 0
    Ij2: float = 0
    Imag: float = 0
    Tmixer: float = 0
    PLL_Lock_V: float = 0
    PLL_Corr_V: float = 0
    PLL_Assm_T: float = 0
    PA_A_Drain_V: float = 0
    PA_B_Drain_V: float = 0
    Source_Power_USB: float = 0
    Source_Power_LSB: float = 0
    Is_LO_Unlocked: bool = False
    Is_RF_Unlocked: bool = False
    
    def getNTText(self, short: bool = True):
        ret = f"pol{self.Pol}: {self.Phot_USB:.2f}, {self.Pcold_USB:.2f}, {self.Phot_LSB:.2f}, {self.Pcold_LSB:.2f}"
        if short:
            return ret
        else:
            return ret + f"\nerrors: {self.Phot_USB_StdErr:.2f}, {self.Pcold_USB_StdErr:.2f}, {self.Phot_LSB_StdErr:.2f}, {self.Pcold_LSB_StdErr:.2f}"
    
    def getIRText(self):
        return f"pol{self.Pol}: {self.PwrUSB_SrcUSB:.2f}, {self.PwrLSB_SrcUSB:.2f}, {self.PwrLSB_SrcLSB:.2f}, {self.PwrUSB_SrcLSB:.2f}"

    def getText(self):
        return self.getNTText() + "\n" + self.getIRText() + f"\natten={self.IF_Attn}, ambient={self.TRF_Hot}, tColdEff={self.TColdLoad}"

    def getVals(self) -> list[any]:
        if self.timeStamp is None:
            self.timeStamp = datetime.now()
            return [
                self.key,
                self.fkCartTest,
                self.fkDUT_Type.value,
                self.timeStamp.strftime('%Y-%m-%d %H:%M:%S'),
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
                self.Source_Power_USB,
                self.Source_Power_LSB,
                1 if self.Is_LO_Unlocked else 0,
                1 if self.Is_RF_Unlocked else 0
            ]

    def getInsertVals(self) -> str:
        """get a string formatted for an INSERT query
        """
        if self.timeStamp is None:
            self.timeStamp = datetime.now()
        return "{},{},'{}',{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
            self.fkCartTest,
            self.fkDUT_Type.value,
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
            self.Source_Power_USB,
            self.Source_Power_LSB,
            1 if self.Is_LO_Unlocked else 0,
            1 if self.Is_RF_Unlocked else 0
        )