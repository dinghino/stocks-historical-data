from datetime import datetime
import click
from termcolor import colored

from simple_term_menu import TerminalMenu


def noop():
    pass

class CLI:
    options = {
        "Start": "2020-5-1",
        "End": datetime.now().date().strftime("%Y-%m-%d"),
        "Tickers": [],
        "Output": "single file",
    }

    def __init__(self):
        self.main_menu = [
            ["[S] Change Start Date", self.get_start_date],
            ["[E] Change End Date", self.get_end_date],
            ["[T] Select Tickers", self.get_tickers],
            ["[O] Change output type", self.get_output_type],
            ["[R] Run scraper", self.launch],
            # ["[Q] Quit", self.quit]
        ]


    def echo_main(self):
        click.clear()
        click.echo(colored("FINRA Volume data scraper\n", "cyan", attrs=['bold']))
        self.print_current_options()
        click.echo()

        values = [el[0] for el in self.main_menu]
        menu = TerminalMenu(values)
            # exit_on_shortcut=False)
        
        choice = menu.show()       # 0 index value
        print(choice)
        print(self.main_menu[choice])
        self.main_menu[choice][1]()

    def launch(self):
        pass
    def quit(self):
        res = click.confirm("Are you sure?", abort=True)
        if not res:
            self.echo_main()

    @click.command()
    # String format, yyyy-mm-dd, defaults to 2020-5-1
    def get_start_date(self):
        try:
            datestr = click.prompt("Enter your start date", default="2020-05-1")
            date = get_date(datestr)
            self.options["Start"] = date.strftime("%Y-%m-%d")
        except ValueError:
            click.confirm(colored("Invalid date format, please try again", attr=['bold']))
            self.get_start_date()
        
    # String format, yyyy-mm-dd, defaults to today
    def get_end_date(self):
        pass

    # space separated list of tickers, can also be empty for all of them
    def get_tickers(self):
        pass

    # define if single file or individual file for each stock
    def get_output_type(self):
        pass

    # output currently selected options
    def print_current_options(self):
        click.echo(colored("Current Options", "cyan", attrs=['bold']))
        for k, v in self.options.items():
            click.echo("{}\t{}".format(colored(k, 'cyan'), colored(v, attrs=['bold'])))

    def current_options(self):
        lines = []
        for k, v in self.options.items():
            lines.append("{}\t{}".format(colored(k, 'cyan'), colored(v, attrs=['bold'])))
        return lines




#################
    # def echo_main():
    #     click.clear()
    #     click.echo("\nFINRA Volume data scraper\n")
    #     print_current_options()
    #     click.echo()
    #     values = [
    #         "[S] Change Start Date",
    #         "[E] Change End Date",
    #         "[T] Select Tickers",
    #         "[O] Change output type",
    #         "[R] Run scraper",
    #         "[Q] Quit"
    #         ]
    #     menu = TerminalMenu(values, exit_on_shortcut=False)
    #     choice = menu.show()       # 0 index value
    

    # def get_main_menu():
    #     return {
    #         "1": { "text": "Edit Options", "func": options_menu },
    #         "2": { "text": "Run Scraper", "func": "" },
    #         "3": { "text": "Exit", "func": noop }
    #     }

    # @click.command()
    # @click.option('-n', '--name', default='user')
    # def cli(name):
    #     click.clear()
    #     click.echo("Hello %s" % name)
    #     echo_main_menu()

    # @click.command()
    # def echo_main_menu():
    
    #     click.echo()
    #     print_current_options()
    #     click.echo()
    #     for idx, v in get_main_menu().items():
    #         click.echo(format_menu(idx, v["text"]))    

    #     choice = click.prompt("\nWhat do you want to do?", default="3")

    #     try:
    #         get_main_menu()[choice][func]()
    #     except:
    #         click.confirm("Invalid options. Try again?", abort=True)
    #         echo_main_menu()

    # @click.command()
    # def options_menu():
    #     click.echo("Options menu!")


def format_menu(idx, text):
    return "{}. {}".format(colored(idx, attrs=['bold']), text)

def get_date(datestr):
    return datetime.strptime(datestr, "%Y-%m-%d").date()

if __name__ == "__main__":
    cli = CLI()
    cli.echo_main()
