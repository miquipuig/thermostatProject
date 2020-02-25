# thermostatProject
# Copyright (C) 2020  Miquel Puig Gibert @miquipuig
 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PIL import Image, ImageTk, ImageSequence
from .import *
   
class ScreenUtilites:
    def __init__(self):     
        logger.info('Init screenUtilites')
    def resizeAnimatedGif(self,path, resizeParams={"percentatgeDecrease": 50}):
        frames = ImageSequence.Iterator(Image.open(path))
        iwidth, iheight=frames[0].size
        width, height=frames[0].size
        action='thumbnail'
        result=[]
        try:
            if(resizeParams):    
                if(resizeParams.get('width')!=None and resizeParams.get('height')!=None):
                    width=int(resizeParams['width'])
                    height=int(resizeParams['height'])
                    action='resize'
                elif(resizeParams.get('width')!=None):
                    height=int(iheight*resizeParams['width']/iwidth)
                    width=int(resizeParams['width'])
                elif(resizeParams.get('height')!=None):
                    width=int(iweight*resizeParams['height']/iheight)
                    height=int(resizeParams['height'])
                elif(resizeParams.get('percentatgeDecrease')!=None):
                    width=int(resizeParams['percentatgeDecrease']*iwidth/100)
                    height=int(resizeParams['percentatgeDecrease']*iheight/100)
        except Exception as ex:
            logger.error('Wrong parameters')
            logger.error(ex)
        for frame in frames:
            image = frame.copy()
            if(action=='resize'):
                image=image.resize([width,height], Image.ANTIALIAS)
            elif(action=='thumbnail'):
                image.thumbnail([width,height], Image.ANTIALIAS)
            yield image

    def animatedGifTk(self,path, resizeparams):
        imageTk=[]
        frames=self.resizeAnimatedGif(path, resizeparams)
        for frame in frames:
            imageTk.append(ImageTk.PhotoImage(frame))
        return imageTk
    
    def resizeImgTk(self,path,width,height):
        return ImageTk.PhotoImage(Image.open(path).resize((width, height), Image.ANTIALIAS))
    
    def coloringImgTk(self,path,width,height,c1,c2,c3):       
        image=Image.open(path).resize((width, height), Image.ANTIALIAS).convert('RGBA')
        data=np.array(image)
        red, green, blue, alpha = data.T
        defined_areas = (red == 0) & (blue == 0) & (green == 0)
        data[..., :-1][defined_areas.T] = (c1, c2, c3)
        data = Image.fromarray(data)
        return ImageTk.PhotoImage(data)
    
su=ScreenUtilites()