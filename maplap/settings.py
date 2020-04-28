"""Settings"""
import sys
import constant as CO


class SettingsParams:
    """Params for settings"""

    # pylint: disable= R0903

    def __init__(self, line_param):
        params = list(line_param.split(","))
        assert len(params) == CO.PARAMS_IN_SETTING
        for i in range(CO.PARAMS_IN_SETTING):
            setattr(self, CO.SETTINGS_PARAM_ATR[i], params[i])


class Settings:
    """Settings struct"""

    def __init__(self):
        with open(CO.DEFAULT_SETTINGS, "r") as file_settings:
            all_lines = list(file_settings)
            assert len(all_lines) == CO.SETTINGS_PARAMS
            for i in range(CO.SETTINGS_PARAMS):
                setattr(self, CO.SETTINGS_ATR[i], SettingsParams(all_lines[i]))
        self.read_settings()

    def read_settings(self):
        """read settings file"""
        try:
            with open(CO.SETTINGS, "r") as file_settings:
                all_lines = list(file_settings)
                assert len(all_lines) == CO.SETTINGS_PARAMS
                for i in range(CO.SETTINGS_PARAMS):
                    name, value = all_lines[i].split()
                    setattr(
                        getattr(self, CO.SETTINGS_ATR[i]),
                        CO.SETTINGS_PARAM_ATR[CO.NAME],
                        name,
                    )
                    setattr(
                        getattr(self, CO.SETTINGS_ATR[i]),
                        CO.SETTINGS_PARAM_ATR[CO.VALUE],
                        value,
                    )
        except IOError:
            print("Left default settings!")

    def save_settings(self):
        """save settings to file"""
        with open(CO.SETTINGS, "w") as file_settings:
            for i in range(CO.SETTINGS_PARAMS):
                param = getattr(self, CO.SETTINGS_ATR[i])
                atr_name = getattr(param, CO.SETTINGS_PARAM_ATR[CO.NAME])
                atr_value = getattr(param, CO.SETTINGS_PARAM_ATR[CO.VALUE])
                print(f"{atr_name} {atr_value}", file=file_settings)
