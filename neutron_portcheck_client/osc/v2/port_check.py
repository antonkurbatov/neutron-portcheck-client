"""Port check action implementation"""

from cliff import columns
from osc_lib.command import command
import six
import yaml


class ValueFormatter(columns.FormattableColumn):
    def human_readable(self):
        if not self._value:
            return 'ok'

        lines = []
        for val in self._value:
            if isinstance(val, dict):
                for idx, key in enumerate(sorted(val.keys())):
                    prefix = '- ' if idx == 0 else '  '
                    lines.append(self.indent('%s:' % key, prefix))
                    lines.append(self.indent(val[key], '    '))
            else:
                lines.append(val)
        return '\n'.join(lines)

    @staticmethod
    def indent(text, prefix):
        return ''.join(prefix+line for line in text.splitlines(True))


class CheckPort(command.ShowOne):
    _description = "Check port"

    port_check_path = "/ports/%s/check"

    def get_parser(self, prog_name):
        parser = super(CheckPort, self).get_parser(prog_name)
        parser.add_argument(
            'port',
            metavar="<port>",
            help="Port to check (name or ID)"
        )
        return parser

    def take_action(self, parsed_args):
        networkclient = self.app.client_manager.network
        client = self.app.client_manager.neutronclient

        port = self.app.client_manager.network.find_port(
            parsed_args.port, ignore_missing=False)
        port_check_path = "/ports/%s/check"
        rv = client.post(port_check_path % (port.id),)
        for key, value in rv.items():
            rv[key] = ValueFormatter(value)

        return zip(*sorted(six.iteritems(rv)))
