with (import <nixpkgs> {});
let

  # All python packages needed for this project
  my-python-packages = python-packages: with python-packages; [
    pyaml
    requests
    beautifulsoup4
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
