"""Port check action implementation"""

from cliff import columns
from osc_lib.command import command
import six

from openstackclient.i18n import _


class CheckPortColumn(columns.FormattableColumn):
    def human_readable(self):
        if not self._value:
            return 'ok'
        out = ''
        for line in self._value:
            out += '- %s\n' % line
        return out.strip()


class CheckPort(command.ShowOne):
    _description = "Check port"

    def get_parser(self, prog_name):
        parser = super(CheckPort, self).get_parser(prog_name)
        parser.add_argument(
            'port',
            metavar="<port>",
            help=_("Port to check (name or ID)")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.neutronclient
        port = self.app.client_manager.network.find_port(
            parsed_args.port, ignore_missing=False)
        rv = client.post("/ports/%s/check" % port.id)['port_check']
        for key, value in rv.items():
            rv[key] = CheckPortColumn(value)
        return zip(*sorted(six.iteritems(rv)))
