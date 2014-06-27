# encoding: utf-8
"""
path.py

Created by Thomas Mangin on 2014-06-27.
Copyright (c) 2009-2013 Exa Networks. All rights reserved.
"""

from exabgp.bgp.message.update.nlri.nlri import NLRI
from exabgp.bgp.message.update.nlri.prefix import Prefix
from exabgp.bgp.message.update.nlri.qualifier.path import PathInfo

class PathPrefix (Prefix,NLRI):
	def __init__ (self,afi,safi,packed,mask,nexthop,action,path=None):
		self.path_info = PathInfo.NOPATH if path is None else path
		self.nexthop = nexthop
		NLRI.__init__(self,afi,safi)
		Prefix.__init__(self,packed,mask)
		self.action = action

	def prefix (self):
		return "%s/%s%s" % (self.ip,self.mask,str(self.path_info) if self.path_info is not PathInfo.NOPATH else '')

	def nlri (self):
		return "%s/%s%s next-hop %s" % (self.ip,self.mask,str(self.path_info) if self.path_info is not PathInfo.NOPATH else '',self.nexthop)

	def pack (self,addpath):
		return self.path_info.pack() + Prefix.pack(self) if addpath else Prefix.pack(self)

	def json (self):
		return '"%s": { %s }' % (Prefix.pack(self),self.path_info.json())

	def index (self):
		return self.pack(True)

	def __len__ (self):
		return Prefix.__len__(self) + len(self.path_info)

	def __str__ (self):
		return "%s next-hop %s" % (self.prefix(),self.nexthop)