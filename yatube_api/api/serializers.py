from rest_framework import serializers


from posts.models import Comment, Post, Group, Follow, User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    following = serializers.CharField(write_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'user', 'following')
        read_only_fields = ('user',)

    def get_user(self, obj):
        return obj.user.username

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['following'] = instance.following.username
        return ret

    def create(self, validated_data):
        username = validated_data.pop('following')
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError()
        validated_data['following'] = user_to_follow
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
        read_only_fields = ('author',)

    def get_author(self, obj):
        return obj.author.username


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post', 'created')

    def get_author(self, obj):
        return obj.author.username
