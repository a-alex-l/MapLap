"""Settings"""
import sys
import constant as C

class SettingsParams:
    """Params for settings"""

    # pylint: disable= R0903

    def __init__(self, line_param):
        params = list(line_param.split(","))
        assert len(params) == C.PARAMS_IN_SETTING
        for i in range(C.PARAMS_IN_SETTING):
            setattr(self, C.SETTINGS_PARAM_ATR[i], params[i])


class Settings:
    """Settings struct"""

    def __init__(self):
        with open(C.DEFAULT_SETTINGS, "r") as file_settings:
            all_lines = list(file_settings)
            assert len(all_lines) == C.SETTINGS_PARAMS
            for i in range(C.SETTINGS_PARAMS):
                setattr(self, C.SETTINGS_ATR[i], SettingsParams(all_lines[i]))
        self.read_settings()

    def read_settings(self):
        """read settings file"""
        try:
            with open(C.SETTINGS, "r") as file_settings:
                all_lines = list(file_settings)
                assert len(all_lines) == C.SETTINGS_PARAMS
                for i in range(C.SETTINGS_PARAMS):
                    name, value = all_lines[i].split()
                    setattr(
                        getattr(self, C.SETTINGS_ATR[i]),
                        C.SETTINGS_PARAM_ATR[C.NAME],
                        name,
                    )
                    setattr(
                        getattr(self, C.SETTINGS_ATR[i]),
                        C.SETTINGS_PARAM_ATR[C.VALUE],
                        value,
                    )
        except IOError:
            print("Left default settings!")

    def save_settings(self):
        """save settings to file"""
        with open(C.SETTINGS, "w") as file_settings:
            for i in range(C.SETTINGS_PARAMS):
                param = getattr(self, C.SETTINGS_ATR[i])
                atr_name = getattr(param, C.SETTINGS_PARAM_ATR[C.NAME])
                atr_value = getattr(param, C.SETTINGS_PARAM_ATR[C.VALUE])
                print(f"{atr_name} {atr_value}", file=file_settings)
