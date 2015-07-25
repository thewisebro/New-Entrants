from lectut.models import Post, Uploadedfile , DownloadLog

DownloadLog.objects.all().delete()
Uploadedfile.objects.all().delete()
Post.objects.all().delete()

print 'Time for a clean slate'
