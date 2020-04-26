"""Settings"""
import sys
import constant as cons


class SettingsParams:
    """Params for settings"""

    # pylint: disable= R0903

    def __init__(self, line_param):
        params = list(line_param.split(","))
        assert len(params) == cons.PARAMS_IN_SETTING
        for i in range(cons.PARAMS_IN_SETTING):
            setattr(self, cons.SETTINGS_PARAM_ATR[i], params[i])


class Settings:
    """Settings struct"""

    def __init__(self):
        with open(cons.DEFAULT_SETTINGS, "r") as file_settings:
            all_lines = list(file_settings)
            assert len(all_lines) == cons.SETTINGS_PARAMS
            for i in range(cons.SETTINGS_PARAMS):
                setattr(self, cons.SETTINGS_ATR[i], SettingsParams(all_lines[i]))
        self.read_settings()

    def read_settings(self):
        """read settings file"""
        try:
            with open(cons.SETTINGS, "r") as file_settings:
                all_lines = list(file_settings)
                assert len(all_lines) == cons.SETTINGS_PARAMS
                for i in range(cons.SETTINGS_PARAMS):
                    name, value = all_lines[i].split()
                    setattr(
                        getattr(self, cons.SETTINGS_ATR[i]),
                        cons.SETTINGS_PARAM_ATR[cons.NAME],
                        name,
                    )
                    setattr(
                        getattr(self, cons.SETTINGS_ATR[i]),
                        cons.SETTINGS_PARAM_ATR[cons.VALUE],
                        value,
                    )
        except IOError:
            print("Left default settings!")

    def save_settings(self):
        """save settings to file"""
        with open(cons.SETTINGS, "w") as file_settings:
            for i in range(cons.SETTINGS_PARAMS):
                param = getattr(self, cons.SETTINGS_ATR[i])
                atr_name = getattr(param, cons.SETTINGS_PARAM_ATR[cons.NAME])
                atr_value = getattr(param, cons.SETTINGS_PARAM_ATR[cons.VALUE])
                print(f"{atr_name} {atr_value}", file=file_settings)
