from traits.api import HasTraits, Instance, List, Str
from traitsui.api import UItem, TreeEditor, View, ModelView, TreeNode


class Experiment(HasTraits):

    name = Str

    view = View('name')


class Simulation(HasTraits):

    name = Str

    view = View('name')


class Study(HasTraits):

    name = Str

    experiments = List(Instance(Experiment))

    view = View('name')


class DataManager(HasTraits):

    studies = List(Instance(Study))

    view = View()


class DataManagerModelView(ModelView):

    traits_view = View(
        UItem('model', editor=TreeEditor(
                nodes=[
                    TreeNode(
                        node_for=[DataManager],
                        label="=Studies",
                        children='studies',
                    ),
                    TreeNode(
                        node_for=[Study],
                        label="name",
                        children='',
                    ),
                    TreeNode(
                        node_for=[Study],
                        label="=Experiments",
                        children='experiments',
                    ),
                    TreeNode(
                        node_for=[Study],
                        label="=Simulations",
                        children='simulations',
                    ),
                    TreeNode(
                        node_for=[Simulation],
                        label="name",
                    ),
                    TreeNode(
                        node_for=[Experiment],
                        label="name",
                    ),
                ]
            )
        ),
        resizable=True,
    )


if __name__ == '__main__':
    data_manager = DataManager(
        studies=[
            Study(
                name='Study A',
                experiments=[
                    Experiment(name='Experiment A1'),
                    Experiment(name='Experiment A2'),
                    Experiment(name='Experiment A3'),
                ],
                simulations=[
                    Simulation(name='Simulation A1'),
                    Simulation(name='Simulation A2'),
                    Simulation(name='Simulation A3'),
                ],
            ),
            Study(
                name='Study B',
                experiments=[
                    Experiment(name='Experiment B1'),
                    Experiment(name='Experiment B2'),
                    Experiment(name='Experiment B3'),
                ],
                simulations=[
                    Simulation(name='Simulation B1'),
                    Simulation(name='Simulation B2'),
                    Simulation(name='Simulation B3'),
                ],
            )
        ]
    )
    model_view = DataManagerModelView(model=data_manager)
    model_view.edit_traits()
