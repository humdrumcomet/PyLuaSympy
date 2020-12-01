newVar{aVar}{
    display = {\alpha_{\beta}},
    value = {5},     #Allow for Matrix <- should ignore comments (largely follow python format
    units = {\hertz},
    description = {a different variable},
    # glsType = {symbol},
    # ensureMath = {true}
}
newVar{anotherVar}{
    value = {100},
    units = {\mega\electronvolt},
    description = {test variable},
}
newVar{c}{
    display = {c},
    value = {3e8},
    units = {\meter\per\second}
    glsType = {cst},
    ensureMath = {false}
}
newEq{anEq}{
    display = {\eta},
    eqt = {aVar**(2/3)},
    units = {\giga\hertz},
    description = {a sub calculation}
    # glsType = {symbol},
    # lambdifyOpts = {numpy},
    # specialExprOpts = {}
}
newEq{scndEq}{
    display = {\delta},
    eqt = {x*anEq*anotherVar/(aVar*c)},
    units = {\kilo\gram},
    description = {calculating the thing}
    # glsType = {symbol},
    # lambdifyOpts = {numpy},
    # specialExprOpts = {}
}
newEq{thrdEq}{
    display = {\rho},
    eqt = {solve(scndEq, aVar)},
    units = {\mega\watt},
}
newEq{frthEq}{
    display = {\rho},
    eqt = {Integral(thrdEq, anotherVar)},
    units = {\mega\watt},
    description = {calculating the thing}
}
newEq{ffthEq}{
    display = {\rho},
    eqt = {Derivative(scndEq, x)},
    units = {\mega\watt},
    description = {calculating the thing}
}
