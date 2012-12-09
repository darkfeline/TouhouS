import unittest

from gensokyo import state
from gensokyo.test import output


class Tester:

    def __init__(self, text):
        self.text = text

    def on_test(self):
        output.write(self.text)


class TestNode(state.StateNode):

    def enter(self, machine):
        print('enter ' + self.tester.text)
        machine.push_handlers(self.tester)

    def exit(self, machine):
        print('exit ' + self.tester.text)
        machine.remove_handlers(self.tester)

TestNode.register_event_type('on_test')


class TestNodeA(TestNode):

    tester = Tester('nodeA')


class TestNodeB(TestNode):

    tester = Tester('nodeB')


class TestNodeC(TestNode):

    tester = Tester('nodeC')


class TestTree(state.StateTree):

    def on_test(self):
        output.write('root')

    def test(self):
        self.dispatch_event('on_test')

    def go(self, to, save):
        self.dispatch_event('on_transition', state.Transition(to, save))

TestTree.register_event_type('on_test')

TestTree.valid_states = (TestNodeA, TestNodeB)
TestNodeB.valid_states = (TestNodeC,)


class TestState(unittest.TestCase):

    def test_state(self):

        def test():
            root.test()
            print(output.text)
            print(state.trace(root))
            print('-' * 20)
            output.clear()

        root = TestTree()
        test()

        root.go(TestNodeA, False)
        test()

        root.go(TestNodeB, False)
        test()

        root.go(TestNodeC, False)
        test()

        root.go(TestNodeA, False)
        test()

        root.go(TestNodeB, False)
        test()

        root.go(TestNodeC, False)
        test()

        root.go(TestNodeA, True)
        test()

if __name__ == '__main__':
    unittest.main()
