with (import (builtins.fetchGit "https://github.com/nixos/nixpkgs") {});
let

  # Path for new token
  token-patch-file = ''
    --- a/gplaycli/gplaycli.py
    +++ b/gplaycli/gplaycli.py
    @@ -184,19 +184,12 @@ class GPlaycli:

     		logger.info("Retrieving token ...")
     		logger.info("Token URL is %s", self.token_url)
    -		email_url = '/'.join([self.token_url, 'email'])
    -		response = requests.get(email_url)
    +		url = '/'.join([self.token_url, 'api/auth'])
    +		response = requests.get(url)
     		if response.status_code == 200:
    -			self.gmail_address = response.text
    -		else:
    -			logger.error("Cannot retrieve email address from token dispenser")
    -			raise ERRORS.TOKEN_DISPENSER_SERVER_ERROR
    -
    -		token_url = '/'.join([self.token_url, 'token/email', self.gmail_address])
    -		response = requests.get(token_url)
    -
    -		if response.status_code == 200:
    -			self.token = response.text
    +			parsed = json.loads(response.text)
    +			self.gmail_address = parsed['email']
    +			self.token = parsed['auth']
     			self.gsfid = hex(self.api.checkin(self.gmail_address, self.token))[2:]
     			logger.info("Email: %s", self.gmail_address)
     			logger.info("Token: %s", self.token)
  '';

  # Build latest gplaycli
  gplaycli-latest = python-packages: with python-packages; (buildPythonPackage rec {
    pname = "gplaycli";
    version = "3.29";
    src = fetchFromGitHub {
      owner = "matlink";
      repo = "gplaycli";
      rev = version;
      sha256 = "10gc1wr259z5hxyk834wyyggvyh82agfq0zp711s4jf334inp45r";
    };
    disabled = !isPy3k;
    patches = [ (writeTextFile { name = "token.patch"; text = token-patch-file; }) ];
    propagatedBuildInputs = [
      libffi pyasn1 clint ndg-httpsclient protobuf requests args
      pyaxmlparser setuptools
      (gpapi-own python-packages)
    ];
  });

  # Build own custom gpapi
  gpapi-own = python-packages: with python-packages; (buildPythonPackage rec {
    version = "0.4.4.5";
    pname = "matlink-gpapi";
    disabled = pythonOlder "3.3";
    src = fetchPypi {
      inherit version pname;
      sha256 = "0s45yb2xiq3pc1fh4bygfgly0fsjk5fkc4wckbckn3ddl7v7vz8c";
    };
    doCheck = false;
    pythonImportsCheck = [ "gpapi.googleplay" ];
    propagatedBuildInputs = [ cryptography protobuf pycryptodome requests ];
  });

  # All python packages needed for this project
  my-python-packages = python-packages: with python-packages; [
    pyaml
    setuptools
    (gplaycli-latest python-packages)
  ];
  python-with-my-packages = python3.withPackages my-python-packages;

in
mkShell {

  # Allow input
  buildInputs = [
    python-with-my-packages
  ];
  propagatedBuildInputs = [
    python-with-my-packages
  ];

}
