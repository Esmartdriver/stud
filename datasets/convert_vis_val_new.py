import json
import numpy as np

video = json.load(open('/nobackup-slow/dataset/my_xfdu/video/vis/train/instances.json'))
all_video_id = list(range(1, len(video['videos']) + 1))
train_video_id = np.random.choice(all_video_id, int(len(all_video_id) * 0.8), replace=False)
test_video_id = list(set(all_video_id) - set(train_video_id))

# num_train_video = int(len(all_video_id) * 0.8)

video_info_train = []
video_info_val = []
images_train = []
images_val = []
id_train = 1
id_val = 1
id_image_train = 1
id_image_val = 1
# breakpoint()
for info in video['videos']:
    if info['id'] in train_video_id:
        video_info_train.append({'id': id_train, 'name': info['file_names'][0].split('/')[0]})
        for index in range(len(info['file_names'])):
            image_info = {'file_name': info['file_names'][index],
                          'height': info['height'], 'width': info['width'], 'id': id_image_train, 'video_id': id_train, 'frame_id': index}
            images_train.append(image_info)
            id_image_train += 1
        id_train += 1
    else:
        video_info_val.append({'id': id_val, 'name': info['file_names'][0].split('/')[0]})
        for index in range(len(info['file_names'])):
            image_info = {'file_name': info['file_names'][index],
                          'height': info['height'], 'width': info['width'], 'id': id_image_val, 'video_id': id_val, 'frame_id': index}
            images_val.append(image_info)
            id_image_val += 1
        id_val += 1
'''
>>> data['images'][101]
{'file_name': 'b1c66a42-6f7d68ca/b1c66a42-6f7d68ca-0000102.jpg', 
'height': 720, 'width': 1280, 'id': 102, 'video_id': 1, 'frame_id': 101}
'''

# breakpoint()
annotation_train = []
annotation_val = []
id_train = 1
id_train_image = 1
id_val = 1
id_val_image = 1
pre_video_train_id = -1 #video['annotations'][0]['video_id']
pre_video_test_id = -1
for index1 in range(len(video['annotations'])):
    if video['annotations'][index1]['video_id'] in train_video_id:
        if pre_video_train_id != video['annotations'][index1]['video_id']:
            cur_video_ann = {}
            for index in range(len(video['annotations'][index1]['bboxes'])):
                cur_video_ann[index] = []

        for index in range(len(video['annotations'][index1]['bboxes'])):
            cur_video_ann[index].append([video['annotations'][index1]['bboxes'][index],
                                        video['annotations'][index1]['areas'][index],
                                        video['annotations'][index1]['iscrowd'],
                                         video['annotations'][index1]['category_id']])
            # annotation_train.append({'id':id_train, 'image_id'})
        if index1 == len(video['annotations']) - 1 or video['annotations'][index1]['video_id'] != video['annotations'][index1+1]['video_id']:
            for key in list(cur_video_ann.keys()):
                instance_id = 1
                # print(id_train_image)
                for item in cur_video_ann[key]:
                    if item[0] is None:
                        annotation_train.append({'id': id_train, 'image_id': id_train_image, 'category_id': item[3],
                                                 'instances_id': instance_id,
                                                 'bdd100k_id': 0, 'occluded': False, 'truncated': False,
                                                 'bbox': item[0], 'area': item[1], 'iscrowd': item[2], 'ignore': 1
                                                 })
                    else:
                        annotation_train.append({'id': id_train, 'image_id': id_train_image, 'category_id': item[3],
                                                 'instances_id': instance_id,
                                                 'bdd100k_id': 0, 'occluded': False, 'truncated': False,
                                                 'bbox': item[0], 'area': item[1], 'iscrowd': item[2], 'ignore': 0
                                                 })

                    instance_id += 1
                    id_train += 1
                id_train_image += 1
        pre_video_train_id = video['annotations'][index1]['video_id']
    else:
        if pre_video_test_id != video['annotations'][index1]['video_id']:
            cur_video_ann = {}
            for index in range(len(video['annotations'][index1]['bboxes'])):
                cur_video_ann[index] = []

        for index in range(len(video['annotations'][index1]['bboxes'])):
            cur_video_ann[index].append([video['annotations'][index1]['bboxes'][index],
                                        video['annotations'][index1]['areas'][index],
                                        video['annotations'][index1]['iscrowd'],
                                         video['annotations'][index1]['category_id']])
            # annotation_train.append({'id':id_train, 'image_id'})
        if index1 == len(video['annotations']) - 1 or video['annotations'][index1]['video_id'] != video['annotations'][index1+1]['video_id']:
            for key in list(cur_video_ann.keys()):
                instance_id = 1
                for item in cur_video_ann[key]:
                    if item[0] is None:
                        annotation_val.append({'id': id_val, 'image_id': id_val_image, 'category_id': item[3],
                                               'instances_id': instance_id,
                                                 'bdd100k_id': 0, 'occluded': False, 'truncated': False,
                                                 'bbox': item[0], 'area': item[1], 'iscrowd': item[2], 'ignore': 1
                                                 })
                    else:
                        annotation_val.append({'id': id_val, 'image_id': id_val_image, 'category_id': item[3],
                                               'instances_id': instance_id,
                                               'bdd100k_id': 0, 'occluded': False, 'truncated': False,
                                               'bbox': item[0], 'area': item[1], 'iscrowd': item[2], 'ignore': 0
                                               })

                    instance_id += 1
                    id_val += 1
                id_val_image += 1
        pre_video_test_id = video['annotations'][index1]['video_id']
'''
{'id': 301, 'image_id': 11, 'category_id': 3,
 'instance_id': 25, 'bdd100k_id': '00122086',
 'occluded': True, 'truncated': False,
 'bbox': [664.2417908674067, 367.9733233708366, 36.698191808020056, 28.229378313861503],
 'area': 1035.9671399832512, 'iscrowd': 0, 'ignore': 0,
 'segmentation':
     [[664.2417908674067, 367.9733233708366, 664.2417908674067, 396.2027016846981, 
     700.9399826754268, 396.2027016846981, 700.9399826754268, 367.9733233708366]]}
'''
# breakpoint()
new_annotation = dict()
new_annotation['categories'] = video['categories']
new_annotation['videos'] = video_info_train
new_annotation['images'] = images_train
new_annotation['annotations'] = annotation_train
json.dump(new_annotation, open('/nobackup-slow/dataset/my_xfdu/video/vis/train/instances_train1.json', 'w'))


new_annotation['videos'] = video_info_val
new_annotation['images'] = images_val
new_annotation['annotations'] = annotation_val
json.dump(new_annotation, open('/nobackup-slow/dataset/my_xfdu/video/vis/train/instances_test1.json', 'w'))


#
# # postprocessing.
train_data = json.load(open('/nobackup-slow/dataset/my_xfdu/video/vis/train/instances_train1.json'))
not_none_image_id = []
for ann in train_data['annotations']:
    if ann['bbox'] is not None:
        not_none_image_id.append(ann['image_id'])
full_image_id = list(range(1, train_data['annotations'][-1]['image_id']+1))
none_image_id_train = list(set(full_image_id).difference(set(not_none_image_id)))


test_data = json.load(open('/nobackup-slow/dataset/my_xfdu/video/vis/train/instances_test1.json'))
not_none_image_id = []
for ann in test_data['annotations']:
    if ann['bbox'] is not None:
        not_none_image_id.append(ann['image_id'])
full_image_id = list(range(1, test_data['annotations'][-1]['image_id']+1))
none_image_id_test = list(set(full_image_id).difference(set(not_none_image_id)))
# breakpoint()

video_info_train = []
video_info_val = []
images_train = []
images_val = []
id_train = 1
id_val = 1
id_image_train = 1
id_image_val = 1
id_real_image_train = 1
id_real_image_val = 1
for info in video['videos']:
    if info['id'] in train_video_id:
        video_info_train.append({'id': id_train, 'name': info['file_names'][0].split('/')[0]})
        temp = 0
        for index in range(len(info['file_names'])):
            if id_image_train not in none_image_id_train:
                image_info = {'file_name': info['file_names'][index],
                              'height': info['height'], 'width': info['width'], 'id': id_real_image_train,
                              'video_id': id_train, 'frame_id': temp}
                temp += 1
                images_train.append(image_info)
                id_real_image_train += 1
            id_image_train += 1
        id_train += 1
    else:
        video_info_val.append({'id': id_val, 'name': info['file_names'][0].split('/')[0]})
        temp = 0
        for index in range(len(info['file_names'])):
            if id_image_val not in none_image_id_test:
                image_info = {'file_name': info['file_names'][index],
                              'height': info['height'], 'width': info['width'], 'id': id_real_image_val,
                              'video_id': id_val, 'frame_id': temp}
                temp += 1
                images_val.append(image_info)
                id_real_image_val += 1
            id_image_val += 1
        id_val += 1
'''
>>> data['images'][101]
{'file_name': 'b1c66a42-6f7d68ca/b1c66a42-6f7d68ca-0000102.jpg', 
'height': 720, 'width': 1280, 'id': 102, 'video_id': 1, 'frame_id': 101}
'''

# breakpoint()
annotation_train = []
annotation_val = []
id_train = 1
id_train_image = 1
id_val = 1
id_val_image = 1
id_real_val_image = 1
id_real_train_image = 1
pre_video_train_id = -1 #video['annotations'][0]['video_id']
pre_video_test_id = -1
for index1 in range(len(video['annotations'])):
    if video['annotations'][index1]['video_id'] in train_video_id:
        if pre_video_train_id != video['annotations'][index1]['video_id']:
            cur_video_ann = {}
            for index in range(len(video['annotations'][index1]['bboxes'])):
                cur_video_ann[index] = []

        for index in range(len(video['annotations'][index1]['bboxes'])):
            cur_video_ann[index].append([video['annotations'][index1]['bboxes'][index],
                                        video['annotations'][index1]['areas'][index],
                                        video['annotations'][index1]['iscrowd'],
                                         video['annotations'][index1]['category_id']])
            # annotation_train.append({'id':id_train, 'image_id'})
        if index1 == len(video['annotations']) - 1 or video['annotations'][index1]['video_id'] != video['annotations'][index1+1]['video_id']:
            for key in list(cur_video_ann.keys()):
                instance_id = 1
                # print(id_train_image)
                for item in cur_video_ann[key]:
                    if item[0] is not None:
                        annotation_train.append({'id': id_train, 'image_id': id_real_train_image, 'category_id': item[3],
                                                 'instances_id': instance_id,
                                                 'bdd100k_id': 0, 'occluded': False, 'truncated': False,
                                                 'bbox': item[0], 'area': item[1], 'iscrowd': item[2], 'ignore': 0
                                                 })
                        instance_id += 1
                        id_train += 1
                if id_train_image not in none_image_id_train:
                    id_real_train_image += 1
                id_train_image += 1
        pre_video_train_id = video['annotations'][index1]['video_id']

    else:
        if pre_video_test_id != video['annotations'][index1]['video_id']:
            cur_video_ann = {}
            for index in range(len(video['annotations'][index1]['bboxes'])):
                cur_video_ann[index] = []

        for index in range(len(video['annotations'][index1]['bboxes'])):
            cur_video_ann[index].append([video['annotations'][index1]['bboxes'][index],
                                        video['annotations'][index1]['areas'][index],
                                        video['annotations'][index1]['iscrowd'],
                                         video['annotations'][index1]['category_id']])
            # annotation_train.append({'id':id_train, 'image_id'})
        if index1 == len(video['annotations']) - 1 or video['annotations'][index1]['video_id'] != video['annotations'][index1+1]['video_id']:
            for key in list(cur_video_ann.keys()):
                instance_id = 1
                for item in cur_video_ann[key]:
                    if item[0] is not None:
                        annotation_val.append({'id': id_val, 'image_id': id_real_val_image, 'category_id': item[3],
                                               'instances_id': instance_id,
                                                 'bdd100k_id': 0, 'occluded': False, 'truncated': False,
                                                 'bbox': item[0], 'area': item[1], 'iscrowd': item[2], 'ignore': 0
                                                 })
                        instance_id += 1
                        id_val += 1
                if id_val_image not in none_image_id_test:
                    id_real_val_image += 1
                id_val_image += 1

        pre_video_test_id = video['annotations'][index1]['video_id']


new_annotation = dict()
new_annotation['categories'] = video['categories']
new_annotation['videos'] = video_info_train
new_annotation['images'] = images_train
new_annotation['annotations'] = annotation_train
json.dump(new_annotation, open('/nobackup-slow/dataset/my_xfdu/video/vis/train/instances_train1.json', 'w'))


new_annotation['videos'] = video_info_val
new_annotation['images'] = images_val
new_annotation['annotations'] = annotation_val
json.dump(new_annotation, open('/nobackup-slow/dataset/my_xfdu/video/vis/train/instances_test1.json', 'w'))
breakpoint()



