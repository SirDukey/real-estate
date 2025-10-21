# Odoo:  real-estate
An Odoo addon for a Real Estate module

This is a module from the official Odoo [tutorial](https://www.odoo.com/documentation/18.0/developer/tutorials/server_framework_101.html)

I have also created another addon called [estate_account](https://github.com/SirDukey/estate_account) which is a link 
module for this module and `account` which allows a sold property to generate an invoice automatically.  
The invoice for the property and buyer is then available at ***invoicing > customers***

## Using the module
I create a folder called `addons` near my forked Odoo repository, I use a `odoo.conf` 
file like this:

    [options]
    db_host = localhost
    db_port = 5432
    db_user = ****
    db_password = ****
    addons_path = <PATH TO YOUR ODOO REPO>/odoo/addons, <PATH TO YOUR ODOO REPO>/addons

then I run Odoo `./odoo/odoo-bin -c odoo.conf`

When developing the module I use the `-u` flag to auto upgrade the module when restarting and
the `--dev` flag to allow browser refresh when working on the views

### Pycharm configuration
I run a Pycharm configuration and use the following flags (adjust as needed), this allows edits to xml files only
requiring a browser refresh to see the changes and a module upgrade each time the configuration is restart, handy for 
developing :grin:

`-c odoo.conf -u real-estate -u estate_account --dev xml`

### VSCode configuration
Create a **.vscode/launch.json** file in the project ***(like ~/Repositories/odoo-fork/.vscode)*** and add this to the
json file to get a configuration started.  Also, don't forget to set the interpreter path :wink:

    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python:Odoo",
                "type": "python",
                "request": "launch",
                "stopOnEntry": false,
                "python": "${command:python.interpreterPath}",
                "console": "integratedTerminal",
                "program": "${workspaceRoot}/odoo/odoo-bin",
                "args": [
                    "--config=${workspaceRoot}/odoo.conf",
                    "-u estate"
                ],
                "cwd": "${workspaceRoot}",
                "env": {},
                "envFile": "${workspaceRoot}/.env",
                "debugOptions": [
                    "RedirectOutput"
                ]
            }
        ]
    }

### Docker
I use docker to host the database and nginx as a reverse proxy, there is a docker compose file
which requires a `.env` file for the database credentials, create this file then run the following:

`docker compose up -d`

This will start up the two containers, access the frontend via http://localhost

### DB init
Initialize a database with the base module:

`python odoo/odoo-bin -d $ODOO_DB --db_host $ODOO_HOST -r $ODOO_USER -w $ODOO_PASS -i base`