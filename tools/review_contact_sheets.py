from pathlib import Path
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent.parent / 'docs/verification/comparisons'
files=sorted(root.glob('*-side-by-side.jpg'))
for start in range(0,len(files),6):
    sheet=Image.new('RGB',(1560,1335),'#e9f0f3')
    draw=ImageDraw.Draw(sheet)
    for i,path in enumerate(files[start:start+6]):
        image=Image.open(path)
        image.thumbnail((760,400))
        x=(i%2)*780; y=(i//2)*445
        draw.text((x+8,y+5),path.stem,fill='black')
        sheet.paste(image,(x+8,y+30))
    sheet.save(root/f'review-sheet-{start//6+1}.jpg',quality=90)
