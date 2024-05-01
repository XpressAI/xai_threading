from xai_components.base import InArg, OutArg, InCompArg, Component, BaseComponent, xai_component
import threading
import copy

@xai_component(color="red")
class ThreadingRunParallel(Component):
    """Runs each path in parallel
    """

    thread1: BaseComponent
    thread2: BaseComponent
    thread3: BaseComponent
    thread4: BaseComponent
    thread5: BaseComponent
    on_finished: BaseComponent

    results: OutArg[list]

    def execute(self, ctx) -> None:
        results_list = []

        def run_thread(thread, results_list, new_ctx):
            thread.do(new_ctx)
            
            results_list.append(new_ctx['thread_result'])

        threads = [
            threading.Thread(target=run_thread, args=(self.thread1, results_list, copy.deepcopy(ctx))),
            threading.Thread(target=run_thread, args=(self.thread2, results_list, copy.deepcopy(ctx))),
            threading.Thread(target=run_thread, args=(self.thread3, results_list, copy.deepcopy(ctx))),
            threading.Thread(target=run_thread, args=(self.thread4, results_list, copy.deepcopy(ctx))),
            threading.Thread(target=run_thread, args=(self.thread5, results_list, copy.deepcopy(ctx)))
        ]

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Set the results to the OutArg
        self.results.value = results_list

        self.on_finished.do(ctx)


@xai_component(color="red")
class ThreadingReturnResult(Component):
    """Sets a result of the thread.
    """

    result: InCompArg[any]

    def execute(self, ctx) -> None:
        ctx["thread_result"] = self.result.value
