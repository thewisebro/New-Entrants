from lectut.models import Post, Uploadedfile , DownloadLog

DownloadLog.objects.all().delete()
Uploadedfile.objects.all().delete()
Post.objects.all().delete()

Print 'Time for a clean slate'
