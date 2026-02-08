

class SlashCommandsCommonTimeTrack:

    @property
    def parameterized_slash_command(self):

        return {
            'spend_full_no_spaces': {
                'spend': True,
                'slash_command': 'spend',
                'command_obj': '1h2m3s',
            },
            'spend_full_spaces': {
                'spend': True,
                'slash_command': 'spend',
                'command_obj': '1h 2m 3s',
            },
            'spend_hour_minute_spaces': {
                'spend': True,
                'slash_command': 'spend',
                'command_obj': '1h 2m',
            },
            'spend_hour_second_spaces': {
                'spend': True,
                'slash_command': 'spend',
                'command_obj': '1h 3s',
            },
            'spend_minute_second_spaces': {
                'spend': True,
                'slash_command': 'spend',
                'command_obj': '5m 3s',
            },
            'spend_hour': {
                'spend': True,
                'slash_command': 'spend',
                'command_obj': '1h',
            },
            'spend_minute': {
                'spend': True,
                'slash_command': 'spend',
                'command_obj': '1m',
            },
            'spend_second': {
                'spend': True,
                'slash_command': 'spend',
                'command_obj': '4s',
            },

            'spent_full_no_spaces': {
                'spend': True,
                'slash_command': 'spent',
                'command_obj': '1h2m3s',
            },
            'spent_full_spaces': {
                'spend': True,
                'slash_command': 'spent',
                'command_obj': '1h 2m 3s',
            },
            'spent_hour_minute_spaces': {
                'spend': True,
                'slash_command': 'spent',
                'command_obj': '1h 2m',
            },
            'spent_hour_second_spaces': {
                'spend': True,
                'slash_command': 'spent',
                'command_obj': '1h 3s',
            },
            'spent_minute_second_spaces': {
                'spend': True,
                'slash_command': 'spent',
                'command_obj': '5m 3s',
            },
            'spent_hour': {
                'spend': True,
                'slash_command': 'spent',
                'command_obj': '1h',
            },
            'spent_minute': {
                'spend': True,
                'slash_command': 'spent',
                'command_obj': '1m',
            },
            'spent_second': {
                'spend': True,
                'slash_command': 'spent',
                'command_obj': '4s',
            },

        }
