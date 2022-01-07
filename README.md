[![PyPI version](https://badge.fury.io/py/indis.svg)](https://badge.fury.io/py/indis)
indis - Icinga native director import service
----------------------------------------------

> This project is currently in beta so API's and functionallity may change. Looking forward to your feedback and pull
> requests.

# Overview 

Indis is a configuration tool for Icinga2 and integrates with the Icinga2 module Director. 
With Indis it possible to read data from other system that provide data that can be used to create
Icinga2 objects, like hosts, hostgroups, services, servicegroups, dependency etc.

The source system is read by Indis source providers. A provider mediate between the source native data model and 
data formats to native Icinga2 objects. A provider is typical something that is customized for a specific source 
system, e.g. a network management system where all routers and switches is managed. 

After the provider has created the icinga objects, the data is processed by a number of configurable processors. 
A processor can typical be logic that enrich or transform the icinga objects in some way, e.g. adding hostgroups, 
adding host and service vars etc.

The final step is to generate the data output, the output data that should be processed by Icinga2 Director.

The major benefit using Indis compared to other integrations like a custom json, a sql table etc, is that all
output from Indis follow the Icinga2 objects structure and naming. This means that all Director configuration, like 
import rules, sync rules, apply rules etc., just needs to operate on the "native" icinga2 object model. 
Instead of writing different rules and configuration depending on the structure of the source, Indis manage that 
separation and abstraction.

**That's why we call it "Icinga native director import service".**

Using Indis it simple to automate Icinga2 configuration with different systems, including gitops driven CI/CD 
pipelines. All the benefits of Icinga director, Icinga DSL and with the power of Python.

> Currently, Indis do not support configuration and management of apply rules. Existing apply rules in Icinga2 
> will of course be executed if matched.

# Use Icinga2 DSL

One key benefit with Icinga2 Director is to use the Icinga DSL to provide logic on how to connect objects together.
Typical the DSL can be used to connect services to hosts. Instead of creating unique services for a host, 
use service templates and apply these based on host attributes like variables, hostgroups etc.

With Indis you get all the benefits of the Icinga DSL, but all the benefits of simple python development to 
extract source system data and create all kinds of Icinga objects.

# Get started

For more hands on and get started check out the `config.yml` and the `demo` provider.
    
    python -m indis -f config.yml -s demo_source


# Output plugins 

Two output plugins are available, a json file plugin and an Icinga2 director API plugin.

## The json file output plugin

The json file output plugin can be used with fileshipper.

Check out the config:
```yaml
output:
  writer: indis.output.json_writer.JsonFileWriter
  configuration:
    directory: /tmp/director
```
The output will be written to the `directory`, with one file for each object typ.

## The Icinga2 director API output plugin

The output plugin will create and update objects using the Icinga2 director REST API.
Delete operations are only supported if a cache store is created. 

Configuration for the output plugin is:
```yaml
output:
  
  writer: indis.output.api_writer.APIWriter
  configuration:
    url: http://localhost/icingaweb2/director
    user: user
    password: password
```
The user must be an existing icinga2 web user with credentials for Director API.


# Source provider

A source provider is implemented as a class that must inherit the Source class.

```pyhton
class Source:

    def __init__(self, config: Configuration, reader: SourceReader):
        self.config = config
        self.reader = reader

    @abstractmethod
    def fetch(self) -> Transfer:
        pass
```
The field `config` give access to all source specific config in the named source section of the yaml configuration 
file. The `reader` field give access to the provider specific reader object that indis creates.

The provider reader class must implement the SourceReader.

```python
class SourceReader:

    def __init__(self, config: Configuration):
        """
        Cofiguration is the section of source
        :param config:
        """
        self.config = config
```
 
Please see the example code in the `demo` directory.

> If you know Mender, you will recognize the programming structure of Indis providers.

# Cache 
If a cache is used it is possible for Indis to understand if object should be removed if not longer existing in 
the source.

## Redis cache
Every key in redis is prefixed with the source identifier. 
Each object type will have a `SET` that keep track of the current configured object of a specific type 
with the format `<source>:<type>`, where type is in plurals e.g. `hosts`.

    127.0.0.1:6379> type demo_source:hosts
    set

For example:

    127.0.0.1:6379> SMEMBERS demo_source:hosts
    1) "www.sunet.se"
    2) "www.opsdis.com"

For each object a key is named by type and name that include the sha of the current configured object 
`<source>:<type>:<name>`

    127.0.0.1:6379> type demo_source:hosts:www.sunet.se
    string

For example:

    127.0.0.1:6379> get "demo_source:hosts:www.sunet.se"
    "4805c225b5543ea62e76503f2778e2f145908c4a26690c83b3d471bc0f9b3e07"


