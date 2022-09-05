### [MOSARCH Home](./) | [Contributors](./people.html) | [Publications](./publications.html) | Toolset

Our toolset aims at software architecture recovery by automatically clustering software modules for increasing modularity and supporting maintainability. The following figure depicts the system overview, where two types of data retrieved from the source code repository are used as input. The first one is the source code, which is analyzed to reveal dependencies among software modules. The second one is the modification history, which reveals software modules that are (often) modified together.

![System Overview](/images/sysoverview.png)

The main modules and the flow of intermediate artifacts are depicted in the figure below. There are 3 main components. The first one performs *Structural Coupling Analysis* to extract *Module Dependencies* by analyzing the *Source Code*. The second one takes *Modification History* and extracts *Module co-changes*. The last component performs *Module Clustering* based on the output of the other two components.

![Flow](/images/flow.png)
