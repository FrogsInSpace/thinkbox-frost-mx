// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0
#include <genlight.h>
#include <imtl.h>
#include <inode.h>
#include <object.h>
#include <render.h>

#include <vraygeom.h>

#if defined( tstring )
#undef tstring
#endif
#if defined( min )
#undef min
#endif
#if defined( max )
#undef max
#endif

class FrostInterface;

class FrostVRenderObject : public VUtils::VRenderObject {
  public:
    FrostVRenderObject( FrostInterface* frost );

    // From VRenderObject
#if VRAY_DLL_VERSION < 0x70000
    VUtils::VRenderInstance* newRenderInstance( INode* node, VUtils::VRayCore* vray, int renderID );
#else
    VUtils::VRenderInstance* newRenderInstance( INode* node, VUtils::VRayCore* vray, int renderID, VUtils::BulkAllocatorInterface *bulkAllocator=nullptr );
#endif
    void deleteRenderInstance( VUtils::VRenderInstance* ri );

    void frameBegin( TimeValue t, VUtils::VRayCore* vray );

  private:
    FrostInterface* m_frost;
};
