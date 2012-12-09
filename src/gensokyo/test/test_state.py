import unittest

from gensokyo import state
from gensokyo.test import output


def trace(tree, pre=''):
    a = pre + str(tree) + '\n'
    for child in tree.children:
        a = ''.join([a, trace(child, pre + '    ')])
    return a


class Tester:

    def __init__(self, text):
        self.text = text

    def on_test(self):
        output.write(self.text)


class TestNode(state.StateNode):

    def enter(self, root):
        output.write('enter ' + str(self))
        root.push_handlers(self.tester)

    def exit(self, root):
        output.write('exit ' + str(self))
        root.remove_handlers(self.tester)

    def __str__(self):
        return self.text


TestNode.register_event_type('on_test')


class TestNodeA(TestNode):

    text = 'nodeA'
    tester = Tester('nodeA')


class TestNodeB(TestNode):

    text = 'nodeB'
    tester = Tester('nodeB')


class TestNodeC(TestNode):

    text = 'nodeC'
    tester = Tester('nodeC')


class TestTree(state.StateTree):

    text = 'root'

    def on_test(self):
        output.write(self.text)

    def test(self):
        self.dispatch_event('on_test')

    def go(self, to, save):
        self.dispatch_event('on_transition', state.Transition(to, save))

    def __str__(self):
        return self.text

TestTree.register_event_type('on_test')

TestTree.valid_states = (TestNodeA, TestNodeB)
TestNodeB.valid_states = (TestNodeC,)


class TestState(unittest.TestCase):

    def test_state(self):

        def test(a):
            root.test()
            output.write('')
            output.write(trace(root))
            print(output.text)
            self.assertEqual(output.text, a)
            print('-' * 40)
            output.clear()

        root = TestTree()
        test('''root

root

''')

        root.go(TestNodeA, False)
        test('''enter nodeA
nodeA
root

root
    nodeA

''')

        root.go(TestNodeB, False)
        test('''exit nodeA
enter nodeB
nodeB
root

root
    nodeB

''')

        root.go(TestNodeC, False)
        test('''enter nodeC
nodeC
nodeB
root

root
    nodeB
        nodeC

''')

        root.go(TestNodeA, False)
        test('''exit nodeC
exit nodeB
enter nodeA
nodeA
root

root
    nodeA

''')

        root.go(TestNodeB, False)
        test('''exit nodeA
enter nodeB
nodeB
root

root
    nodeB

''')

        root.go(TestNodeC, False)
        test('''enter nodeC
nodeC
nodeB
root

root
    nodeB
        nodeC

''')

        root.go(TestNodeA, True)
        test('''exit nodeC
exit nodeB
enter nodeA
nodeA
root

root
    nodeB
        nodeC
    nodeA

''')

if __name__ == '__main__':
    unittest.main()
