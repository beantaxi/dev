using System;
using System.Threading;
using System.Threading.Tasks;

namespace AsyncLab
{
    sealed public class App
    {
        public static void Main (string[] args)
        {
        		Console.WriteLine("About to await ...");
        		SlowpokeCaller().Wait();
        		Console.WriteLine("Done.");
        }


        private static Task SlowpokeCaller ()
        {
        		Task t = Task.Run(() => Slowpoke());	

        		return t;
        }


        private static void Slowpoke ()
        {
        		Console.WriteLine("About to do something slowly ...");
        		// Task.Delay(1000).Wait();
        		Thread.Sleep(2000);
        		Console.WriteLine("Slow operation complete.");
        }
    }
}
