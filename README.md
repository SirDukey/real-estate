# real-estate
An Odoo addon for a Real Estate module

This is a module from the official Odoo [tutorial](https://www.odoo.com/documentation/18.0/developer/tutorials/server_framework_101.html)

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

I run a Pycharm configuration and use the following flags:
`-c odoo.conf -u estate --dev xml`