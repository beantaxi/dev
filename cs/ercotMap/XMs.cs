using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using HtmlAgilityPack;
using NLog;

namespace cs
{
    static public class XMs
    {
        static private Logger logger = LogManager.GetCurrentClassLogger();
        static public FileInfo Download (this Uri url)
        {
            FileInfo path = null;
            using (var http = new HttpClient())
            {
                HttpResponseMessage resp = http.GetResponse(url);
                resp.EnsureSuccessStatusCode();
                byte[] content = resp.GetContent();
                path = content.WriteToTempFile();

            }

            return path;
        }


        static private HttpResponseMessage GetResponse (this HttpClient http, Uri url)
        {
            logger.Trace($"Downloading {url} ...");
            Task<HttpResponseMessage> responseTask = http.GetAsync(url);
            responseTask.Wait();
            HttpResponseMessage resp = responseTask.Result;
            resp.LogStatus();

            return resp;
        }

        static byte[] GetContent (this HttpResponseMessage resp)
        {
            Task<byte[]> contentTask = resp.Content.ReadAsByteArrayAsync();
            contentTask.Wait();
            byte[] content = contentTask.Result;

            return content;
        }

        static public string GetParentUriString (this Uri uri)
        {
            return uri.AbsoluteUri.Remove(uri.AbsoluteUri.Length - uri.Segments[uri.Segments.Length -1].Length - uri.Query.Length);
        }        

        static private string GetStatusLine (this HttpResponseMessage resp)
        {
            string statusLine = $"{(int)resp.StatusCode} {resp.StatusCode} {resp.IsSuccessStatusCode} {resp.ReasonPhrase}";

            return statusLine;
        }


        static public Uri GetPngUrl (this HtmlDocument html)
        {
            Uri url = null;

            string xpPng = "//div[@class='portlet-light']/table/tr[3]/td/table/tr[1]/td[1]/img";
            HtmlNode hit = html.DocumentNode.SelectSingleNode(xpPng);
            if (hit == null)
            {
                logger.Warn("No hit");
            }
            else
            {
                string src = hit.Attributes["src"].Value ;
                logger.Trace($"src={src}");
                string sUrl = "http://www.ercot.com/content/cdr/contours/rtmLmp.html";
                int iLastSlash = sUrl.LastIndexOf('/');
                sUrl = sUrl.Substring(0, iLastSlash);
                logger.Trace($"sUrl={sUrl}");
                sUrl = $"{sUrl}/{src}";
                logger.Trace($"sUrl={sUrl}");
                url = new Uri(sUrl);
            }

            logger.Trace($"url={url}");
            return url;
        }


        static public DateTime? GetTimestamp (this HtmlDocument html)
        {
            DateTime? dtTimestamp = null;
            string xpTimestamp = "//td[@class='dashboard']/div[@class='datestamp']";
            var hit = html.DocumentNode.SelectSingleNode(xpTimestamp);
            logger.Trace($"hit={hit}");
            if (hit != null)
            {
                string s = hit.InnerText;
                logger.Trace($"hit.InnerText={hit.InnerText}");
                string prefix = "Last Updated: ";
                string sTimestamp = s.Substring(prefix.Length);
                logger.Trace($"{sTimestamp}=sTimestamp");
                string fmtTimestamp = "MMM dd, yyyy HH:mm";
                DateTime dt;
                if (DateTime.TryParseExact(sTimestamp, fmtTimestamp, CultureInfo.InvariantCulture, DateTimeStyles.None, out dt) || DateTime.TryParse(fmtTimestamp, out dt))
                {
                    dtTimestamp = dt;
                }
                else 
                {
                    logger.Warn("No timestamp found.");
                }
            }
            else
            {
                logger.Warn("No hit found.");
            }

            logger.Trace($"dtTimestamp={dtTimestamp}");
            return dtTimestamp;
        }


        static private void LogStatus (this HttpResponseMessage resp)
        {
            string statusLine = resp.GetStatusLine();
            if (resp.IsSuccessStatusCode)
            {
                logger.Trace(statusLine);
            }
            else
            {
                logger.Warn(statusLine);
            }
        }


        static private FileInfo WriteToTempFile (this byte[] buf )
        {
            var path = new FileInfo(Path.GetTempFileName());
            logger.Trace($"Writing {buf.Length} byte(s) to {path} ...");
            using (FileStream stream = File.Open(path.FullName, FileMode.Truncate, FileAccess.Write))
            {
                var o = new BinaryWriter(stream);
                o.Write(buf);
            }

            return path;
        }


        static public IDictionary<string, Uri> ParseLinks (this HtmlDocument html)
        {
            var linkMap = new Dictionary<string, Uri>();

            string xpKmlLinks = "//td[@class='dashboard'][2]/div[@class='datestamp']/a";
            HtmlNodeCollection links = html.DocumentNode.SelectNodes(xpKmlLinks);
            if (links == null || links.Count == 0)
            {
                logger.Warn("no hit");
            }
            else
            {
                string scheme = Constants.URL_RtmLmp.Scheme;
                string host = Constants.URL_RtmLmp.Host;
                int port = Constants.URL_RtmLmp.Port;

                foreach (var hit in links)
                {
                    string href = hit.Attributes["href"].Value;
                    Uri uri;
                    if (href.StartsWith('/'))
                    {
                        uri = new UriBuilder(scheme, host, port, href).Uri;
                    }
                    else
                    {
                        string sUri = $"{Constants.URL_RtmLmp.GetParentUriString()}/{href}";
                        uri = new Uri(sUri);
                    }
                    Console.WriteLine($"Parent url={Constants.URL_RtmLmp.GetParentUriString()}");
                    string text = hit.InnerText;
                    linkMap[text] = uri;
                }
            }

            return linkMap;
        }            
    }
}