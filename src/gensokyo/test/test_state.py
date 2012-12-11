import unittest

from gensokyo import state
from gensokyo.test import locator


def trace(tree, pre=''):
    a = pre + str(tree) + '\n'
    for child in tree.children:
        a = ''.join([a, trace(child, pre + '    ')])
    return a


class Tester:

    def __init__(self, text):
        self.text = text

    def on_test(self):
        locator.output.write(self.text)


class TestNode(state.StateNode):

    def enter(self):
        locator.output.write('enter ' + str(self))
        locator.testhub.push_handlers(self.tester)

    def exit(self):
        locator.output.write('exit ' + str(self))
        locator.testhub.remove_handlers(self.tester)

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
        locator.output.write(self.text)

    def go(self, to, save):
        self.dispatch_event('on_transition', state.Transition(to, save))

    def __str__(self):
        return self.text


TestTree.valid_states = (TestNodeA, TestNodeB)
TestNodeB.valid_states = (TestNodeC,)


class TestState(unittest.TestCase):

    def test_state(self):

        def test(a):
            locator.testhub.test()
            locator.output.write('')
            locator.output.write(trace(root))
            print(locator.output.text)
            self.assertEqual(locator.output.text, a)
            print('-' * 40)
            locator.output.clear()

        root = TestTree()
        locator.testhub.push_handlers(root)
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
