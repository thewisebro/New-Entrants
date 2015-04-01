<ul class="list-group emoji-search scrollable-menu">
  <li mentio-menu-item="emoji" ng-repeat="emoji in items" class="list-group-item clearfix">
    <div class="emoji-photo"><img ng-src="{{emoji.imageUrl}}"></div>
    <div class="text-primary" ng-bind-html="emoji.name | mentioHighlight:typedTerm:'menu-highlighted' | unsafe"></div>
  </li>
</ul>
