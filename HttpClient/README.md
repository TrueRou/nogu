# Nogu Http Test Unit

## Requirements
- Pycharm Professional or JetBrains Http Cli

The JetBrains Http Cli can be downloaded with `curl -f -L -o ijhttp.zip "https://jb.gg/ijhttp/latest"`  
The ZIP distribution requires `JDK 17` to be installed.

#### About how to use it
[JetBrains Official HTTP Client CLI Help](https://www.jetbrains.com/help/pycharm/2023.1/http-client-cli.html)  

## Usage
1. Fill in all params in file `http-client.private.env.json`
2. Set up your dev environment  
In pycharm you just need to select it on the top of opened `.http` file  
If you use Http Cli, refer to the manual above.
3. Open `http-client-osuApiV2.http`, all requests we need are in it.(May not all, because we haven't need it now.)
4. Run `@name Client Credentials Grant` Request, it will set the environment with osu api v2 token, expired in 24h.
5. Now you can use any other apis.

## Development
You just need to add new request in `http-client-osuApiV2.http`.

- All http requests are seperated with `###`.
- Code with `> {% ... %}` is a javascript function that handle something after post-processing.  
- Code with `< {% ... %}` is the pre-request script, can be used to initialize variable.  
- `>> {{file}}` will write the response to `{{file}}`, `>>!` to force write or overwrite it.
- `//` or `#` is the annotation.
- Request name can be defined with `@name {{name}}`