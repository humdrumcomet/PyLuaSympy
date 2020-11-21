newVar{aVar}{
    display = {\alpha_{\beta}},
    value = {5},     #Allow for Matrix <- should ignore comments (largely follow python format
    units = {\hertz},
    description = {a different variable},
    # glsType = {symbol},
    # ensureMath = {true}
}
newVar{anotherVar}{
    display = {\phi^{\omega}},
    value = {100},
    units = {\mega\electronvolt},
    description = {test variable},
    # glsType = {symbol},
    # ensureMath = {true}
}
newVar{c}{
    display = {c},
    value = {3e8},
    units = {\meter\per\second}
    description = {speed of light},
    glsType = {constant},
    # ensureMath = {true}
}
newEq{anEq}{
    display = {\eta},
    eqt = {aVar**(2/3)},
    units = {\giga\hertz},
    # glsType = {symbol},
    # lambdifyOpts = {numpy},
    # specialExprOpts = {}
}
newEq{scndEq}{
    display = {\delta},
    eqt = {x*anEq*anotherVar/c},
    units = {\kilo\gram},
    # glsType = {symbol},
    # lambdifyOpts = {numpy},
    # specialExprOpts = {}
}
