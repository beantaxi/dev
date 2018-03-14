using System;
using System.Globalization;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using HtmlAgilityPack;
using NLog;

namespace cs
{
    class Program
    {
        
        static private Logger logger = LogManager.GetCurrentClassLogger();
        static public void Main(string[] args)
        {
            try
            {
                FileInfo path = Constants.URL_RtmLmp.Download();
                logger.Info($"Downloaded to {path}");

                ParseHtml(path);

                logger.Info("Done.");
            }
            catch (Exception ex)
            {
                logger.Error(ex);
                Environment.Exit(1);
            }
        }

        static private void ParseHtml (FileInfo path)
        {
            using (FileStream stream = File.Open(path.FullName, FileMode.Open, FileAccess.Read))
            {
                var html = new HtmlDocument();
                html.Load(stream);
                DateTime? dtTimestamp = html.GetTimestamp();
                logger.Info($"dtTimestamp={dtTimestamp}");

                Uri urlPng = html.GetPngUrl();
                logger.Info($"urlPng={urlPng}");

                string filePrefix = dtTimestamp.Value.ToString("HHmm");
                logger.Info($"filePrefix={filePrefix}");

                ParseKmlLinks(html);
            }
        }

        static private void ParseKmlLinks (HtmlDocument html)
        {
            string xpKmlLinks = "//td[@class='dashboard'][2]/div[@class='datestamp']/a";
            HtmlNodeCollection links = html.DocumentNode.SelectNodes(xpKmlLinks);
            if (links == null || links.Count == 0)
            {
                logger.Warn("no hit");
            }
            else
            {
                foreach (var hit in links)
                {
                    string href = hit.Attributes["href"].Value;
                    string text = hit.InnerText;
                    logger.Info($"{text} {href}");
                }
            }
        }
    }
}