using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using HtmlAgilityPack;
using Microsoft.Extensions.Configuration;
using NLog;
using NLog.Config;

namespace cs
{
    class Program
    {
        
        static private Logger logger = LogManager.GetCurrentClassLogger();
        static public void Main(string[] args)
        {
            try
            {
                var cfgBuilder = new ConfigurationBuilder();
                
                var config = new XmlLoggingConfiguration("nlog.config");
                Console.WriteLine($"{config.AllTargets.Count} target(s)");
                FileInfo path = Constants.URL_RtmLmp.Download();
                logger.Info($"Downloaded to {path}");

                ContourMapData data = ParseHtml(path);
                logger.Info($"Timestamp => {data.Timestamp}");
                logger.Info($"PNG URL => {data.PngUrl}");
                logger.Info($"PNG File => {data.PngFile}");
                logger.Info("KML Link Map");
                foreach (var kv in data.KmlLinkMap)
                {
                    logger.Info($"\t{kv.Key} => {kv.Value}");
                }
                logger.Info("KML File Map");
                foreach (var kv in data.KmlFileMap)
                {
                    logger.Info($"\t{kv.Key} => {kv.Value}");
                }

                logger.Info("Done.");
            }
            catch (Exception ex)
            {
                logger.Error(ex);
                Environment.Exit(1);
            }
        }

        static private ContourMapData ParseHtml (FileInfo path)
        {
            var data = new ContourMapData();
            using (FileStream stream = File.Open(path.FullName, FileMode.Open, FileAccess.Read))
            {
                var html = new HtmlDocument();
                html.Load(stream);
                DateTime? dtTimestamp = html.GetTimestamp();
                logger.Info($"dtTimestamp={dtTimestamp}");
                data.Timestamp = dtTimestamp.Value;

                Uri urlPng = html.GetPngUrl();
                logger.Info($"urlPng={urlPng}");
                data.PngUrl = urlPng;
                FileInfo f = urlPng.Download();
                logger.Info($"Downloaded PNG to {f}");
                data.PngFile = f;

                string filePrefix = dtTimestamp.Value.ToString("HHmm");
                logger.Info($"filePrefix={filePrefix}");

                IDictionary<string, FileInfo> linkMap = DownloadKmlLinks(html, data);
                foreach (var kv in linkMap)
                {
                    logger.Info($"{kv.Key} => {kv.Value}");
                }
            }

            return data;
        }

        static private IDictionary<string, FileInfo> DownloadKmlLinks (HtmlDocument html, ContourMapData data)
        {
            var fileMap = new Dictionary<string, FileInfo>();
            logger.Info("Links ...");
            IDictionary<string, Uri> linkMap = html.ParseLinks();
            foreach (var kv in linkMap)
            {
                FileInfo f = kv.Value.Download();
                fileMap[kv.Key] = f;
            }

            data.KmlLinkMap = linkMap;
            data.KmlFileMap = fileMap;

            return fileMap;
        }

        static public void LogLink (IDictionary<string, Uri> linkMap, string key)
        {
            Uri uri = linkMap[key];
            logger.Info($"Link for {key} => {uri}");
        }
    }
}