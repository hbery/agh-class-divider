# Diagram

Diagram przedstawiający model programowania liniowego,
pozwalający w optymalny sposób zadowolić jak największą liczbę studentów.

![Diagram](./Class_Divider_diagram_dark.png#gh-dark-mode-only)
![Diagram](./Class_Divider_diagram_light.png#gh-light-mode-only)

Ideą jest zbudowanie modelu matematycznego pozwalającego optymalnie wyznaczyć grupy dla studentów w skończonym czasie.
Zakładamy ogólną liczbę zmiennych binarnych w modelu na poziomie 2000-6000.

Model wykonywany również w Pythonie w bibliotece [PuLP](https://coin-or.github.io/pulp/) z użyciem grafowych połączeń przy użyciu biblioteki [NetworkX](https://networkx.org/documentation/stable/index.html).
