import wikiResource

class Triple:
  def __init__(self,data):
    resourcesroot = "http://101companies.org/resources/"
    self.subject = wikiResource.WikiResource("", "", data[0].replace(resourcesroot, ""), False)
    self.predicate = data[1].replace("http://101companies.org/property/", "")
    self.object = data[2]
    self.toInternal = self.object.startswith(resourcesroot)
    if self.toInternal:
      self.object = wikiResource.WikiResource("", "", self.object.replace(resourcesroot, ""), False)
