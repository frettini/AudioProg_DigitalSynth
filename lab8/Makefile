EXTNAME := Cfilter
EXTSRCS := Cfilter.cxx
USRNAME := macuser

WRAPSRC := $(EXTNAME)_wrap.cxx
WRAPOBJ := $(WRAPSRC:.cxx=.o)
EXTOBJS := $(EXTSRCS:.cxx=.o)


_$(EXTNAME).so : $(EXTOBJS) $(WRAPOBJ)
	g++ -dynamiclib $(WRAPOBJ) $(EXTOBJS) -o _$(EXTNAME).dylib -undefined dynamic_lookup  -L/Users/$(USRNAME)/Documents/anaconda_swig_files/lib -I/Users/$(USRNAME)/Documents/anaconda_swig_files/python3.7m -I/Users/$(USRNAME)/Documents/anaconda_swig_files/lib/python3.7/site-packages/numpy/core/include  
	ln _$(EXTNAME).dylib _$(EXTNAME).so
		
$(WRAPOBJ) : $(WRAPSRC)
	g++ -std=c++11 -fPIC -c $(WRAPSRC) -DNDEBUG -g -fwrapv -O3 -Wall -I/Users/$(USRNAME)/Documents/anaconda_swig_files/python3.7m  -I/Users/$(USRNAME)/Documents/anaconda_swig_files/lib/python3.7/site-packages/numpy/core/include 
	


$(WRAPSRC) : 
	g++ -std=c++11 -fPIC -c $(EXTSRCS)
	swig -c++ -python $(EXTNAME).i


#$(EXTOBJS) :
#	g++ -std=c++11 -fPIC -c $(EXTSRCS)
#	swig -c++ -python $(EXTNAME).i
			


%.o: %.cxx
	g++ -c -fPIC $(CFLAGS) $*.cxx -o $*.o
	g++ -MM $(CFLAGS) $*.cxx > $*.d
	@mv -f $*.d $*.d.tmp
	@sed -e 's|.*:|$*.o:|' < $*.d.tmp > $*.d
	@cp -f $*.d $*.d.tmp
	@sed -e 's/.*://' -e 's/\\$$//' < $*.d.tmp | fmt -1 | \
          sed -e 's/^ *//' -e 's/$$/:/' >> $*.d
	@rm -f $*.d.tmp

.PHONY: clean
clean:
	rm -f $(EXTOBJS) $(WRAPSRC) $(WRAPOBJ) _$(EXTNAME).so $(EXTNAME).py _$(EXTNAME).dylib $(EXTSRCS:.cxx=.d)