__YAMLB64DECODE_DIR="${0:A:h}"

function yamlb64decode() {
    python3 ${__YAMLB64DECODE_DIR}/yamlb64decode.py $@
}

alias -g V="| yamlb64decode"
