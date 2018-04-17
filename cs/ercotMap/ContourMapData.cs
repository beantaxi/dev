using System;
using System.Collections.Generic;
using System.IO;

namespace cs
{
    public class ContourMapData
    {
        public DateTime Timestamp {get; set;}

        public Uri PngUrl { get; set; }

        public FileInfo PngFile { get; set; }

        public IDictionary<string, FileInfo> KmlFileMap { get; set; }

        public IDictionary<string, Uri> KmlLinkMap { get; set; }
    }
}